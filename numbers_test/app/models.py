from django.db import models

class Order(models.Model):
    index_in_table = models.PositiveIntegerField()
    order_id = models.PositiveIntegerField()
    incoming_date = models.DateField()
    total_cost_in_dollars = models.PositiveIntegerField()
    total_cost_in_rubles = models.PositiveIntegerField()
    total_cost_in_rubles_after_comma = models.PositiveIntegerField()

    def __str__(self):
        return str(self.order_id)


class CurrencyRate(models.Model):
    currency_name = models.CharField(max_length=100)
    currency_rate_to_rubles = models.PositiveIntegerField()

    def __str__(self):
        return str(self.currency_name)


class BotMessage(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="messages")
    message_send_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.order_id)