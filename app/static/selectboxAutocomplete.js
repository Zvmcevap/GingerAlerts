$(document).ready(function () {
    $('.selectbox').select2({
        placeholder: 'Stranke',
        allowClear: true,
        maximumSelectionLength: 1,
        width: 'resolve'
    });


    $('.selectbox-multi').select2({
        placeholder: 'Izberi Stranke',
        width: 'resolve'
    });

    $('#zelengumb').click(function () {
        $('.selectbox-multi').attr('required', true);
        $('.blue-group').show();
        $('.green-group').hide()
    });
    $('#modergumb').click(function () {
        $('.selectbox-multi').attr('required', false);
        $('.selectbox-multi').val(null).trigger('change');
        $('.blue-group').hide();
        $('.green-group').show()
    });

    jQuery.fn.extend({
        insertAtCaret: function (myValue) {
            return this.each(function (i) {
                if (document.selection) {
                    //For browsers like Internet Explorer
                    this.focus();
                    var sel = document.selection.createRange();
                    sel.text = myValue;
                    this.focus();
                } else if (this.selectionStart || this.selectionStart == '0') {
                    //For browsers like Firefox and Webkit based
                    var startPos = this.selectionStart;
                    var endPos = this.selectionEnd;
                    var scrollTop = this.scrollTop;
                    this.value = this.value.substring(0, startPos) + myValue + this.value.substring(endPos, this.value.length);
                    this.focus();
                    this.selectionStart = startPos + myValue.length;
                    this.selectionEnd = startPos + myValue.length;
                    this.scrollTop = scrollTop;
                } else {
                    this.value += myValue;
                    this.focus();
                }
            });
        }
    });
    $("#ime-stranke").click(function () {
        $('#template').insertAtCaret('{ime_stranke}');
    });
    $("#cas-termina").click(function () {
        $('#template').insertAtCaret('{čas_termina}');
    });
});
