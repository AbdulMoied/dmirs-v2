### Multiselect filter 

def resolve_csvfilter(queryset, name, value):
    lookup = { f'{name}__in': value.split(",") }
    queryset = queryset.filter(**lookup)
    return queryset