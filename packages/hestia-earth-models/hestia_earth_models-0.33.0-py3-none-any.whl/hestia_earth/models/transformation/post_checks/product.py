"""
Product value

This model calculates the value of every `Product` by taking the value of the `Input` with the same `term`.
Note: this model also substract `Emissions` for `Input` with `units` = `kg N`.
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.tools import list_sum
from hestia_earth.utils.model import filter_list_term_type

from hestia_earth.models.log import logShouldRun
from hestia_earth.models.utils.constant import Units, convert_to_N
from hestia_earth.models.utils.blank_node import get_N_total, get_KG_total, get_total_value
from hestia_earth.models.utils.term import get_lookup_value

REQUIREMENTS = {
    "Transformation": {
        "term.termType": "excretaManagement",
        "inputs": [{"@type": "Input", "value": "", "term.termType": "excreta"}],
        "products": [{"@type": "Product", "value": ""}]
    }
}
RETURNS = {
    "Transformation": {
        "products": [{"@type": "Product", "value": ""}]
    }
}
LOOKUPS = {
    "emission": "causesExcretaMassLoss"
}

EMISSIONS_VALUE = {
    Units.KG_N.value: lambda inputs, emissions: list_sum(
        get_N_total(inputs)
    ) - list_sum([convert_to_N(e) for e in emissions]),
    Units.KG.value: lambda inputs, emissions: list_sum(
        get_KG_total(inputs)
    ) - list_sum(get_total_value(emissions))
}


def _product_value(product: dict, inputs: list, emissions: list):
    units = product.get('term', {}).get('units')
    return EMISSIONS_VALUE[units](inputs, emissions) if units in EMISSIONS_VALUE else list_sum(get_total_value(inputs))


def _run_product(product: dict, inputs: list, emissions: list):
    inputs = [i for i in inputs if i.get('term', {}).get('@id') == product.get('term', {}).get('@id')]
    should_replace = len(product.get('value', [])) == 0
    return {
        **product,
        **({'value': [_product_value(product, inputs, emissions)]} if should_replace else {})
    }


def _run(transformation: dict):
    emissions = transformation.get('emissions', [])
    # only some emissions will reduce the mass
    emissions = [e for e in emissions if get_lookup_value(e.get('term', {}), LOOKUPS['emission'])]
    inputs = filter_list_term_type(transformation.get('inputs', []), TermTermType.EXCRETA)
    return [_run_product(p, inputs, emissions) for p in transformation.get('products', [])]


def _should_run(transformation: dict):
    term_id = transformation.get('term', {}).get('@id')
    should_run = transformation.get('term', {}).get('termType') == TermTermType.EXCRETAMANAGEMENT.value
    logShouldRun(transformation, 'transformation/post_checks', term_id, should_run)
    return should_run


def run(transformation: dict):
    products = _run(transformation) if _should_run(transformation) else []
    return {**transformation, **({'products': products} if len(products) > 0 else {})}
