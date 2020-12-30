// https://stackoverflow.com/a/16654226
$.fn.replaceOptions = function(options) {
    var self, $option;

    this.empty();
    self = this;

    $.each(options, function(index, option) {
        $option = $("<option></option>")
            .attr("value", option.value)
            .text(option.text);
        self.append($option);
    });
};

function handleProjectChange(keepSelection = true) {
    var project_id = $('#project_selector').val();
    var project_categories = [{value: "", text: "--------"}];
    project_categories = project_categories.concat(categories.filter((e) => e.project.toString() === project_id));
    if (keepSelection) {
        var previous_category = $('#category_selector').val();
    }
    $('#category_selector').replaceOptions(project_categories);
    if (keepSelection) {
        var selector = '#category_selector option[value="' + previous_category + '"]';
        $(selector).attr('selected','selected');
    }
}

$('#project_selector').change(handleProjectChange);

$(document).ready(function() {
    $('#datetimepicker').datetimepicker({
        format: 'Y-m-d H:i', //TODO: can we localize the format?
        inline: true,
        step: 30,
        defaultDate:new Date()
    });
    handleProjectChange(true);
});
