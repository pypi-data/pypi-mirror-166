from django import forms
from ml_ibge.ibge import IBGE
from requests.exceptions import ConnectionError


class MLIBGECitiesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MLIBGECitiesForm, self).__init__(*args, **kwargs)
        try:
            default_choices = [("", "Escolha uma opção")]
            self.fields["state"] = forms.ChoiceField(
                label="Estado",
                choices=default_choices + self._choices_states(),
            )
            self.fields["city"] = forms.ChoiceField(label="Cidade", choices=[])

            if "state" in self.data:
                state = self.data.get("state")
                self.fields["city"].choices = default_choices + self._choices_cities(state)
            elif self.instance.pk:
                self.fields["city"].choices = default_choices + self._choices_cities(self.instance.state)
                self.initial["city"] = self.instance.city
        except ConnectionError:
            pass

    def _choices_states(self) -> list[tuple[str, str]]:
        return [(state["UF-sigla"], state["UF-nome"]) for state in IBGE.get_states()]

    def _choices_cities(self, uf) -> list[tuple[str, str]]:
        return [(city["distrito-nome"], city["distrito-nome"]) for city in IBGE.get_cities(uf)]
