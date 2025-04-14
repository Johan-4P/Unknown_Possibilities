def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['time'].widget.attrs['min'] = '09:00'
    self.fields['time'].widget.attrs['max'] = '17:00'
