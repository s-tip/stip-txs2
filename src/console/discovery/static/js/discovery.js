$(function () {
    $("#btn-modify-discovery").click(function () {
        $('#modify-discovery-title').val($('#text-discovery-title').text());
        $('#modify-discovery-description').val($('#text-discovery-description').text());
        $('#modify-discovery-contact').val($('#text-discovery-contact').text());
        $('#modify-discovery-default').val($('#text-discovery-default-title').text());
        $('#modal-modify-discovery').modal();
    });

    $("#check-no-default").change(function(){
        $('#modify-discovery-default').prop('disabled',($(this).prop('checked')));
    });

    $("#btn-modify-discovery-changes").click(function(){
        var f = $('#form-modify-discovery');
        var default_api_root = null;
        if ($("#check-no-default").prop('checked') == false){
            default_api_root = $('#modify-discovery-default').val();
        }
        var data = {
            title: $('#modify-discovery-title').val(),
            description: $('#modify-discovery-description').val(),
            contact: $('#modify-discovery-contact').val(),
            default: default_api_root
        };
        $('<input>').attr({
            'type': 'hidden', 'name': 'data', 'value': JSON.stringify(data)
        }).appendTo(f);
        f.submit();
    });
});
