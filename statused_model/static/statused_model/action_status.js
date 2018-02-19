(function($) {
$(document).on('ready', function() {
    $("select.status_action_choices").each(function( index ) {
        $( this ).parent().css("padding-left", "10px");
    });

    function hide_status_action_choices(){
        $("select.status_action_choices").each(function( index ) {
            $( this ).parent().hide();
        });
    };

    $('select[name="action"]', '#changelist-form').on('change', function() {
        hide_status_action_choices();
        if ($(this).val().startsWith('set_statusfield_')){
            var selector = 'select[name="' + $(this).val() + '"]';
            $(selector).parent().show();
        }
    });
$('select[name="action"]', '#changelist-form').change();
});
})(django.jQuery);