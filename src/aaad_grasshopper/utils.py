def dobj_names_map_original_to_flat(dataset):
    """
    Returns a dictionary mapping the original names of dataobjects to the flattened names (as used in 'DataObject.column_df').
    """

    mapping = {}
    for dobj in dataset.dataobjects:
        mapping[dobj.name_org] = dobj.columns_df
    return mapping


def dobj_names_map_flat_to_original(dataset):
    """
    Returns a dictionary mapping the "flattened" names of data objects (as used in 'DataObject.column_df') to the original names.
    The output is of a form of flat_name : [original_name, index], where index indicates the position in the aggregated list.
    """
    mapping = {}
    for dobj in dataset.dataobjects:
        for i, c in enumerate(dobj.columns_df):
            mapping[c] = [dobj.name_org, i]
    return mapping
