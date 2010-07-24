
$('#login_button').click(function() {
                             $('#login_form').submit();
});

$('#site_search_input, #login_username, #login_password').css('color', '#666');

$('#site_search_input').val('Site Search');
$('#login_username').val('Username');
$('#login_password').val('Password');


$('#site_search_input, #login_username, #login_password').focus(function() {
                                                                    $(this).val('');
                                                                    $(this).css('color', '#000');
                                                                });


