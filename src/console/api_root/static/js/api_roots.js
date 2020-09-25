$(function () {
    var DEFAULT_MAX_CONTENT_LENGTH = '104857600';


    function get_api_root_tr(btn){
        return btn.parents('.tr-api-root');
    };

    function get_api_root_name(btn){
        return get_api_root_tr(btn).children('.th-api-root-name').text()
    };

    function get_api_root_title(btn){
        return get_api_root_tr(btn).children('.th-api-root-title').text()
    };

    function get_api_root_description(btn){
        return get_api_root_tr(btn).children('.th-api-root-description').text()
    };

    function get_api_root_max_content_length(btn){
        return get_api_root_tr(btn).children('.th-api-root-max-content-length').text()
    };

    function get_api_root_collections(btn){
        var api_root_name = get_api_root_name(btn);
        var collections = [];
        $.ajax({
            url: '/api_roots/get_collections/',
            method: 'get',
            async: false,
            data:{
                api_root_name: api_root_name
            },
            cache: false,
        }).done(function (data) {
            collections = data['collections'];
        }).fail(function(XMLHttpRequest, textStatus, errorThrown){
            var msg = XMLHttpRequest.statusText+ ': ' + XMLHttpRequest.responseText;
            alert(msg);
        });
        return collections;
    };

    function get_api_root_users(btn){
        var api_root_name = get_api_root_name(btn);
        var collections = [];
        $.ajax({
            url: '/api_roots/get_users/',
            method: 'get',
            async: false,
            data:{
                api_root_name: api_root_name
            },
            cache: false,
        }).done(function (data) {
            users = data['users'];
        }).fail(function(XMLHttpRequest, textStatus, errorThrown){
            var msg = XMLHttpRequest.statusText+ ': ' + XMLHttpRequest.responseText;
            alert(msg);
        });
        return users;
    };

    $(".btn-modify-api-root").click(function () {
        var collections = get_api_root_collections($(this));
        var users = get_api_root_users($(this));
        $('#modify-api-root-name').val(get_api_root_name($(this)));
        $('#modify-api-root-title').val(get_api_root_title($(this)));
        $('#modify-api-root-description').val(get_api_root_description($(this)));
        $('#modify-api-root-max-content-length').val(get_api_root_max_content_length($(this)));
        modal_create_modify_api_root(true, 'modify', collections, users);
    });

    $("#btn-create-api-root").click(function () {
        $('#modify-api-root-name').val('');
        $('#modify-api-root-title').val('');
        $('#modify-api-root-description').val('');
        $('#modify-api-root-max-content-length').val(DEFAULT_MAX_CONTENT_LENGTH);
        modal_create_modify_api_root(false, 'create', [], null);
    })

    function modal_create_modify_api_root(name_disabled, action, collections, users){
        $('#modify-api-root-name').prop('disabled',name_disabled);
        $('#modify-api-root-action').val(action);
        if(action == 'modify'){
            $('.check-col-id').each(function(index, element){
                if(collections.indexOf($(element).data('col-id')) == -1){
                    $(element).prop('checked', false)
                }else{
                    $(element).prop('checked', true)
                }
            });
            $('.check-users').each(function(index, element){
                if(users.indexOf($(element).data('username')) == -1){
                    $(element).prop('checked', false)
                }else{
                    $(element).prop('checked', true)
                }
            });
        }
        $('#modal-api-root-modify').modal();
    };

    $("#btn-create-modify-changes").click(function(){
        var f = $('#form-create-modify-api-root');

        var collections = [];
        $('.check-col-id').each(function(index, element){
            if($(element).prop('checked')){
                collections.push($(element).data('col-id'));
            }
        });

        var users = [];
        $('.check-users').each(function(index, element){
            if($(element).prop('checked')){
                users.push($(element).data('username'));
            }
        });

        var data = {
            api_root_name: $('#modify-api-root-name').val(),
            title: $('#modify-api-root-title').val(),
            description: $('#modify-api-root-description').val(),
            max_content_length: $('#modify-api-root-max-content-length').val(),
            action: $('#modify-api-root-action').val(),
            collections: collections,
            users: users
        };
        $('<input>').attr({
            'type': 'hidden', 'name': 'data', 'value': JSON.stringify(data)
        }).appendTo(f);
        f.submit();
    });

    $(".btn-delete-api-root").click(function(){
        var api_root_name = get_api_root_name($(this));
        var confirm_content = 'Delete api_root (' + api_root_name + ')?';
        ret = confirm(confirm_content);
        if (ret == false){
            return;
        }
        var f = $('#form-delete-api-root');
        var data = {
            api_root_name: api_root_name
        };
        $('<input>').attr({
            'type': 'hidden', 'name': 'data', 'value': JSON.stringify(data)
        }).appendTo(f);
        f.submit();
    });
});