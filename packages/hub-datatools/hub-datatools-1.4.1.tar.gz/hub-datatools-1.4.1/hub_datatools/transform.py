from typing import Dict, Iterable, Optional, Protocol

import pandas as pd
from pandas import DataFrame, Series

NA_VALUES = ('', '-', 'NS/NC', 'NA')

TRUE_VALUES = ('Sí', 'TRUE')
FALSE_VALUES = ('No', 'FALSE')


class TransformFn(Protocol):
    def __call__(self, data: Series, **kwargs) -> Series:
        pass


def transform_opt(data: Series, na_values: Iterable[str] = NA_VALUES,
                  inplace: bool = False, **kwargs) -> Series:
    if not inplace:
        data = data.copy()

    data.replace(na_values, None, inplace=True)
    return data


def transform_enum(data: Series, values: Dict[str, str] = None, **kwargs) -> Series:
    if values:
        data = data.map(values)
    return data.astype('category')


def transform_bool(data: Series, true_values: Iterable[str] = TRUE_VALUES,
                   false_values: Iterable[str] = FALSE_VALUES, inplace: bool = False, **kwargs) -> Series:
    if not inplace:
        data = data.copy()

    data.replace(true_values, True, inplace=True)
    data.replace(false_values, False, inplace=True)
    return data


def transform_strip(data: Series, **kwargs) -> Series:
    return data.str.strip()


def transform_remove_double_space(data: Series, **kwargs) -> Series:
    return data.str.replace('(\s)+', r'\1', regex=True)


def transform_fix_common_typos(data: Series, **kwargs) -> Series:
    data = data.str.replace(r'^º', '', regex=True)
    data = data.str.replace(r'º$', '', regex=True)
    return data


def transform_fix_date_typos(data: Series, **kwargs) -> Series:
    data = data.str.replace(r'^\?\?', '01', regex=True)
    data = data.str.replace(r'-+', '/', regex=True)
    data = data.str.replace(r'^(\d{1,2})/(\d{1,2})(\d{2,4})$', r'\1/\2/\3', regex=True)
    return data


def transform_datetime(data: Series, yearfirst: bool = False, dayfirst: bool = True,
                       format: str = None, exact: bool = True, **kwargs):
    return pd.to_datetime(data, yearfirst=yearfirst, dayfirst=dayfirst,
                          format=format, exact=exact)


def transform_date(data: Series, **kwargs):
    return transform_datetime(data, **kwargs).dt.date


def transform_number(data: Series, errors: str = 'raise', downcast: str = None, **kwargs) -> Series:
    data = data.str.replace(',', '.', regex=False)
    data = data.str.replace('..', '.', regex=False)
    return pd.to_numeric(data, errors=errors, downcast=downcast)


def transform_cast(type: str) -> TransformFn:
    return lambda df, **kwargs: df.astype(type)


def apply_transform_pipeline(df: DataFrame, field: str, pipeline: Iterable[TransformFn],
                             inplace: bool | str = False, **kwargs) -> DataFrame:
    data = df[field]
    for fn in pipeline:
        data = fn(data, **kwargs, inplace=inplace)

    if inplace:
        df[inplace if isinstance(inplace, str) else field] = data

    return data


OPT_STRING_PIPELINE = (
    transform_strip,
    transform_remove_double_space,
)

OPT_BOOL_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_bool,
)

OPT_DATE_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_fix_date_typos,
    transform_date,
)

OPT_DATETIME_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_fix_date_typos,
    transform_datetime,
)

OPT_ENUM_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_enum,
)

OPT_NUMBER_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_number,
)

OPT_INT_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_number,
    transform_cast('Int64'),
)

OPT_FLOAT_PIPELINE = (
    transform_strip,
    transform_fix_common_typos,
    transform_opt,
    transform_number,
    transform_cast('Float64'),
)
