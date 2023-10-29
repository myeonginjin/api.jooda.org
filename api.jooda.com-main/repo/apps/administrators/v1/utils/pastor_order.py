from apps.churchs.models import Church, ChurchPastor

pastor_order_interval = 10000


class PastorOrder:
    @staticmethod
    def get_last_order(church: Church) -> int:
        church_pastors = ChurchPastor.objects.all()
        church_pastors = church_pastors.filter(church=church).order_by("order")
        if church_pastors.exists():
            return church_pastors.last().order
        return 0

    @staticmethod
    def get_next_order(current_order: int) -> int:
        return current_order + pastor_order_interval

    @staticmethod
    def refresh_order(
        church_pastors: ChurchPastor, pastor: ChurchPastor, index: int
    ) -> None:
        church_pastors = list(church_pastors.exclude(id=pastor.id))
        church_pastors.insert(index, pastor)
        current_order = 0
        for pastor in church_pastors:
            current_order = PastorOrder.get_next_order(current_order)
            pastor.order = current_order
        ChurchPastor.objects.bulk_update(church_pastors, ["order"])

    def get_changed_order(church_pastors: ChurchPastor, index: int) -> int:
        if index == 0:
            return church_pastors[index].order // 2
        elif index >= church_pastors.count():
            return PastorOrder.get_next_order(church_pastors.last().order)

        interval = (church_pastors[index].order - church_pastors[index - 1].order) // 2
        if interval:
            return church_pastors[index].order - interval

        return interval
