private async Task CargarOrden(Instrument instrument, Order or, int cantidad)
{
    if (_providersApi == null)
        return;

    or.InstrumentId = instrument;
    or.CancelPrevious = true;
    or.Side = Side.Sell;
    or.Type = Primary.Data.Orders.Type.Market;
    or.Quantity = cantidad;
    or.Expiration = Expiration.Day; 

    var orderId = await _providersApi.SubmitOrder(_loginInfo?.Cuenta, or);
    if (orderId != null && string.IsNullOrEmpty(orderId.ClientOrderId) == false)
    {
        ToLog($"ID ultima orden enviada: {orderId.ClientOrderId}");

        var orderStatus1 = await _providersApi.GetOrderStatus(orderId);
        Console.WriteLine("{0}", orderStatus1.Status.ToString());
        if (orderStatus1.Status.ToString().Equals("Filled") == false)
        {
            ToLog(string.Format("ERROR. Orden {0} => {1} Descripcion: {2}", orderId.ClientOrderId, orderStatus1.Status, orderStatus1.StatusText));
        }
        ToLog(string.Format("La orden {0} esta {1}: {2}", orderStatus1.ClientOrderId, orderStatus1.Status, orderStatus1.StatusText));
    }
}



private async Task ActualizarAccountInfo()
{
    if (_providersApi != null && _loginInfo != null)
    {
        _accountData = null;
        _diasCaucion = 0;
        _accountData = await _providersApi.GetAccountStatement(_loginInfo.Cuenta);
        if (_accountData != null)
        {
            lblARS.Text = _accountData.DetailedAccountReports[CI].CurrencyBalance["ARS"].Available.ToString("C");
            lblUSD.Text = _accountData.DetailedAccountReports[CI].CurrencyBalance["USD D"].Available.ToString("C");

            DateTime settlement = _accountData.DetailedAccountReports[CI].SettlementDate;
            lblSettlementDate.Text = settlement.ToString("dd/MM/yyyy");

            // OJO: Si hoy no es laborable, este valor no es correcto.
            _diasCaucion = Common.FeriadosAR.MinimoDeDiasParaCaucionar(dtpFecha.Value);
            lblDias.Text = _diasCaucion.ToString();

            // TODO: Hacer parametrizable....
            // Decreto que lo maximo a caucionar es el 98% de los montos disponibles.
            _maximoCaucionableARS = Convert.ToDecimal(0.98) * _accountData.DetailedAccountReports[CI].CurrencyBalance["ARS"].Available;
            _maximoCaucionableUSD = Convert.ToDecimal(0.98) * _accountData.DetailedAccountReports[CI].CurrencyBalance["USD D"].Available;
        }
    }
}

