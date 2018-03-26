$(document).ready(function() {
    $('#datetimepicker').datetimepicker({
        format: 'Y-m-d H:i', //TODO: can we localize the format?
        inline: true,
        step: 30,
        defaultDate:new Date()
    });
});
