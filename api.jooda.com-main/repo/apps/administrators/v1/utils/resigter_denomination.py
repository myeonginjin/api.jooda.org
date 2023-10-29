from apps.churchs.models import Church, ChurchDenomination


def resigter_denomination(church: Church, denomination_name: str) -> None:
    if denomination_name:
        try:
            denomination = ChurchDenomination.objects.get(name=denomination_name)
        except ChurchDenomination.DoesNotExist:
            denomination = ChurchDenomination.objects.create(name=denomination_name)
        church.denomination = denomination
        church.save(update_fields=["denomination"])
