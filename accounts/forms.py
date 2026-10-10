from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from phonenumber_field.formfields import SplitPhoneNumberField

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire d'inscription personnalisé basé sur UserCreationForm de Django.
    Il intègre les champs additionnels : email, phone_number, et picture.
    """
    # Utilisation du champ de téléphone international avec un widget adapté
    phone_number = SplitPhoneNumberField(
        required=False,
        region="FR",
        label="Numéro de téléphone"
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'picture')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['username'].help_text = (
            "150 caractères maximum. Lettres, chiffres et @/./+/-/_ uniquement."
        )
        self.fields['password1'].label = "Mot de passe"
        self.fields['password1'].help_text = (
            "Utilisez au moins 8 caractères, évitez les mots de passe courants "
            "et n'utilisez pas uniquement des chiffres."
        )
        self.fields['password2'].label = "Confirmation du mot de passe"
        self.fields['password2'].help_text = (
            "Saisissez le même mot de passe une seconde fois pour vérification."
        )