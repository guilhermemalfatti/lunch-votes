/**
 * Created by malfatti on 22/02/17.
 */
        $(document).ready(function(){
             var NowMoment = moment().format('DD/MM/YYYY');
             $('#datetimeLabel').text(NowMoment);
             $('#datetime').val(NowMoment);

             $('#result-content').hide()

        });

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

            });

            // stop the form from submitting the normal way and refreshing the page
            event.preventDefault();
        });