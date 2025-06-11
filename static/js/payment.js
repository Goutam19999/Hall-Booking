
function togglePaymentFields() {
    const selected = $('#id_payment_method').val();
    if (selected === 'upi') {
        $('#upi_fields').show();
        $('#card_fields').hide();
        $('#upi_fields input').attr('required', true);
        $('#card_fields input').removeAttr('required');
    } else {
        $('#upi_fields').hide();
        $('#card_fields').show();
        $('#card_fields input').attr('required', true);
        $('#upi_fields input').removeAttr('required');
    }
}

$(document).ready(function () {
    togglePaymentFields(); // Run on page load
    $('#id_payment_method').change(togglePaymentFields); // Run on change
});
