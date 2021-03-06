// Generated by CoffeeScript 1.10.0
(function() {
  var activePage, clearImage, next, pagi, prev, previewImage, removeUser, search, usersUrl;

  activePage = null;

  usersUrl = null;

  removeUser = function(url) {
    $.confirm({
      text: 'Вы действительно хотите удалить пользователя?',
      confirm: function(button) {
        $.post(url, {
          csrfmiddlewaretoken: csrftoken
        }, function(data) {
          window.location = data.redirect_url;
        });
      },
      title: 'Удаление пользователя',
      confirmButton: 'Удалить',
      cancelButton: 'Отмена'
    });
  };

  prev = function() {
    var search;
    search = $('#search').val();
    activePage = activePage === 0 ? activePage : activePage - 1;
    document.location = usersUrl + '?page=' + activePage + ';search=' + search;
  };

  next = function() {
    var current, search;
    search = $('#search').val();
    current = $('li.active[data-pagi=\'true\']');
    if (!current.attr('data-max')) {
      activePage = activePage + 1;
    }
    document.location = usersUrl + '?page=' + activePage + ';search=' + search;
  };

  pagi = function(ind) {
    var search;
    search = $('#search').val();
    document.location = usersUrl + '?page=' + ind + ';search=' + search;
  };

  search = function() {
    var search;
    search = $('#search').val();
    document.location = usersUrl + '?search=' + search;
  };

  clearImage = function() {
    $('#profile_img').attr('src', "/assets/system/dist/img/anonymous-160x160.gif");
    $("#fileupload").val('');
    $('#fileupload_avatar').val('');
    $('#add-btn').show();
    $('#clear-btn').hide();
  };

  previewImage = function(event) {
    var input, reader;
    input = event.target;
    if (input.files && input.files[0]) {
      reader = new FileReader();
      reader.onload = function(e) {
        $('#profile_img').attr('src', e.target.result);
        $('#fileupload_avatar').val(e.target.result);
      };
      reader.readAsDataURL(input.files[0]);
      $('#add-btn').hide();
      return $('#clear-btn').show();
    }
  };

  $(document).ready(function() {
    activePage = $('#active_num').val();
    usersUrl = $('#users_table').attr('data-url');
    $('[name="birth_date"]').datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
      forseParse: false,
      keyboardNavigation: false
    });
    $('[name="phone"]').inputmask('99999999999');
    if ($('#fileupload')) {
      $("#fileupload").on('change', previewImage);
    }
  });

}).call(this);

//# sourceMappingURL=users.js.map
