def from_enum_choice(enum,all_captial = True):
    not_included_fields = ['choices','choices_dict'];
    choices_field = 'choices';
    choice_dict = {};
    if not choices_field in dir(enum):
        choices = sorted([(getattr(enum, f), f.upper() if all_captial else f.capit) for f in dir(enum) if (f not in not_included_fields) and (not f.startswith('_'))]);
        for k,v in choices:
            choice_dict[k] = v;
        setattr(enum,choices_field, choices);
        setattr(enum,'choices_dict', choice_dict);
    else:
        for k,v in enum.choices:
            choice_dict[k] = v;
        setattr(enum,'choices_dict', choice_dict);
    return getattr(enum, choices_field);