$(document).ready(function () {
    $('.edit-modal-opener').click(function () {
        var url = $(this).data('url');
        $.get(url, function (data) {
            $('#Modal .modal-content').html(data);
            $('#Modal').modal('show');
            $('.close-modal').click(function (event) {
                $('#Modal').modal('hide');
            });
            $('#submit').click(function (event) {
                event.preventDefault();
                $.post(url, data = $('#ModalForm').serialize(), function (data) {
                    if (data.status == 'ok') {
                        $('#Modal').modal('hide');
                        location.reload();
                    } else {
                        $('.help-block').remove()
                        $('<p class="help-block">' + data.status + '</p>').insertAfter("label[for='" + data.key + "']");
                        $('#Modal').animate({
                            scrollTop: $('.help-block').offset().top - $('#Modal').offset().top + $('#Modal').scrollTop()
                        });
                    }
                })
            });
        })
    });
});

function showNewClientForm (e) {
    if (e.checked) {
        $('#exist_client_form').hide();
        $('#new_client_form').show();
    }
    else {
        $('#new_client_form').hide();
        $('#exist_client_form').show();
    }
}

function showNewBrandForm (e) {
    if (e.checked) {
        $('#exist_brand_form').hide();
        $('#new_brand_form').show();
    }
    else {
        $('#new_brand_form').hide();
        $('#exist_brand_form').show();
    }
}