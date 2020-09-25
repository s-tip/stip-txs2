$(function () {
    function get_collection_tr(btn){
        return btn.parents('.tr-collection');
    };

    function get_collection_id(btn){
        return get_collection_tr(btn).children('.th-collection-id').text();
    };

    function get_collection_title(btn){
        return get_collection_tr(btn).children('.th-collection-title').text();
    };

    function get_collection_description(btn){
        return get_collection_tr(btn).children('.th-collection-description').text();
    };

    function get_collection_alias(btn){
        return get_collection_tr(btn).children('.th-collection-alias').text();
    };

    function get_collection_can_read(btn){
        return get_collection_tr(btn).children('td').children('.check-collection-can-read').prop('checked');
    };

    function get_collection_can_write(btn){
        return get_collection_tr(btn).children('td').children('.check-collection-can-write').prop('checked');
    };

    $(".btn-modify-collection").click(function () {
        var d = {col_id: get_collection_id($(this))};
        var can_read_communities = null;
        var can_write_community  = null;
        $.ajax({
            url: '/collections/get_access_authority/',
            method: 'post',
            async: false,
            data: d,
            cache: false,
        }).done(function (data) {
            can_read_communities = data['can_read_communities'];
            can_write_community  = data['can_write_community'];
        }).fail(function(XMLHttpRequest, textStatus, errorThrown){
            var msg = XMLHttpRequest.statusText+ ': ' + XMLHttpRequest.responseText;
            alert(msg);
            return;
        });

        $('#modify-collection-id').val(get_collection_id($(this)));
        $('#modify-collection-title').val(get_collection_title($(this)));
        $('#modify-collection-description').val(get_collection_description($(this)));
        $('#modify-collection-alias').val(get_collection_alias($(this)));

        $('#modify-collection-can-read').prop('checked', get_collection_can_read($(this)));
        $('.check-can-read-community').prop('disabled', get_collection_can_read($(this)) == false);
        if(can_read_communities != null){
            $('.check-can-read-community').each(function(index, element){
                if(can_read_communities.indexOf($(element).data('community-name')) > -1){
                    $(element).prop('checked', true);
                }else{
                    $(element).prop('checked', false);
                }
            });
        }
        else{
            $('.check-can-read-community').prop('checked', false);
        };


        $('#modify-collection-can-write').prop('checked', get_collection_can_write($(this)));
        $('.radio-can-write-community').prop('disabled', get_collection_can_write($(this)) == false);
        if(can_write_community != null){
            $('.radio-can-write-community').each(function(index, element){
                if(can_write_community == $(element).val()){
                    $(element).prop('checked', true);
                }else{
                    $(element).prop('checked', false);
                }
            });
        }
        modal_create_modify_collection(true, 'modify');
    });

    $("#btn-create-collection").click(function () {
        $('#modify-collection-id').val('');
        $('#modify-collection-title').val('');
        $('#modify-collection-description').val('');
        $('#modify-collection-alias').val('');
        $('#modify-collection-can-read').prop('checked', false);
        $('.check-can-read-community').prop('disabled', true);
        $('.check-can-read-community').prop('checked', false);
        $('#modify-collection-can-write').prop('checked', false);
        $('.radio-can-write-community').prop('disabled', true);
        $('.radio-can-write-community').prop('checked', false);
        modal_create_modify_collection(false, 'create');
    })

    function modal_create_modify_collection(id_disabled, action){
        $('#modify-collection-id').prop('disabled',id_disabled);
        if(action == 'create'){
            $('#div-modify-collection-gen-uuid').show();
        }
        $('#modify-collection-action').val(action);
        $('#modal-collection-modify').modal();
    };

    $('#div-modify-collection-gen-uuid').click(function(){
        $.ajax({
            url: '/collections/generate_uuid/',
            method: 'get',
            cache: false,
        }).done(function (data) {
            $('#modify-collection-id').val(data['uuid']);
        }).fail(function(XMLHttpRequest, textStatus, errorThrown){
            var msg = XMLHttpRequest.statusText+ ': ' + XMLHttpRequest.responseText;
            alert(msg);
        });
    });

    $("#btn-create-modify-changes").click(function(){
        var f = $('#form-create-modify-collection');
        var can_read_communities = [];
        $('.check-can-read-community').each(function(index, element){
            if($(element).prop('checked')){
                can_read_communities.push($(element).data('community-name'));
            };
        });

        var can_write_community = null;
        $('.radio-can-write-community').each(function(index, element){
            if($(element).prop('checked')){
                can_write_community = $(element).val();
                return false;
            };
        });

        var data = {
            id: $('#modify-collection-id').val(),
            title: $('#modify-collection-title').val(),
            description: $('#modify-collection-description').val(),
            alias: $('#modify-collection-alias').val(),
            can_read: $('#modify-collection-can-read').prop('checked'),
            can_write: $('#modify-collection-can-write').prop('checked'),
            can_read_communities: can_read_communities,
            can_write_community: can_write_community,
            action: $('#modify-collection-action').val(),
        };
        $('<input>').attr({
            'type': 'hidden', 'name': 'data', 'value': JSON.stringify(data)
        }).appendTo(f);
        f.submit();
    });

    $(".btn-delete-collection").click(function(){
        var col_id = get_collection_id(($(this)));
        var confirm_content = 'Delete colletion (' + col_id + ')';
        ret = confirm(confirm_content);
        if (ret == false){
            return;
        }
        var f = $('#form-delete-collection');
        var data = {
            col_id: col_id
        };
        $('<input>').attr({
            'type': 'hidden', 'name': 'data', 'value': JSON.stringify(data)
        }).appendTo(f);
        f.submit();
    });

    $("#modify-collection-can-read").change(function(){
        $('.check-can-read-community').prop('disabled',($(this).prop('checked') == false));
    });

    $("#modify-collection-can-write").change(function(){
        $('.radio-can-write-community').prop('disabled',($(this).prop('checked') == false));
    });
});