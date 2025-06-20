function calculate_booking_total() {
    const numAdults = parseFloat(document.getElementById('booking_number_adults').value) || 0;
    const priceAdult = parseFloat(document.getElementById('booking_price_adults').value) || 0;
    const numChildren = parseFloat(document.getElementById('booking_number_children').value) || 0;
    const priceChild = parseFloat(document.getElementById('booking_price_children').value) || 0;
    const discount = parseFloat(document.getElementById('booking_discount').value) || 0;
    
    const subtotal = (numAdults * priceAdult) + (numChildren * priceChild);
    const total = subtotal - discount;
    
    console.log(total.toFixed(2));
    document.getElementById('booking_total').value = total.toFixed(2);
}

function calculate_invoice_total() {
    const service_value = parseFloat(document.getElementById('invoice_service_value').value) || 0;
    const taxes = parseFloat(document.getElementById('invoice_taxes_value').value) || 0;
    const discount = parseFloat(document.getElementById('invoice_discount_value').value) || 0;
    
    const total = service_value + taxes - discount;
    
    document.getElementById('invoice_total_amount').value = total.toFixed(2);
}