/**
 * Created by malfatti on 22/02/17.
 */
        //restore the main disclaimer
        function restoreDisclaimer(){
            $('.alert-vote').removeClass('alert-success alert-warning alert-info');
            $('.alert-vote').addClass('alert-info');
            $('.disclaimer').text('The user can only vote once a day.');
        }

        //event of vote - send the vote to backend
        $('#vote').click(function(){
             $.ajax({
                type        : 'GET', // define the type of HTTP verb we want to use (POST for our form)
                url         : 'availablerest', // the url where we want to POST
                dataType    : 'json', // what type of data do we expect back from the server
                encode          : true
            }).done(function(data) {
                $('#restaurant').find('option').remove();
                 $.each(data, function (index, value) {
                    $('#restaurant').append($('<option/>', {
                        value: value,
                        text : value
                    }));
                });
            });

            restoreDisclaimer();
        });

         // process the form
        $('form').submit(function(event) {

            // get the form data
            var formData = {
                'employee'              : $('select[name=employee]').val(),
                'restaurant'             : $('select[name=restaurant]').val(),
                'datetime'    : $('input[name=datetime]').val()
            };

            // process the form
            $.ajax({
                type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
                url         : 'recordvote', // the url where we want to POST
                data        : formData, // our data object
                dataType    : 'json', // what type of data do we expect back from the server
                encode          : true
            })
            .done(function(data) {
                $('.alert-vote').removeClass('alert-success alert-warning alert-info');
                // log data to the console so we can see
                if (data.status == 'success'){
                    $('.alert-vote').addClass('alert-success');
                }else{
                    $('.alert-vote').addClass('alert-warning');
                }
                $('.disclaimer').text(data.message);

                $('.disclaimer').fadeOut(500);
                $('.disclaimer').fadeIn(500);

            });

            // stop the form from submitting the normal way and refreshing the page
            event.preventDefault();
        });