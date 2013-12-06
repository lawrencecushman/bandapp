
$(document).ready(function() {
    //toggle `popup` / `inline` mode
    jQuery.fn.editable.defaults.mode = 'popup';

    // make editable things editable
    $('.editable').editable('toggleDisabled');
    $('.song-delete').tooltip({content: 'Delete song'});

    // clear performer form
    function clearPerformerForm(){
        var form = $('#form');
        form.find("select").prop('selectedIndex',0);
        form.find("input").val('');
    }

    function clearAlbumForm(){
        var form = $('#albumForm');
        form.find("input").val('');
    }

    function clearSongForm() {
        var form = $('#discography').find('.song-form');
        form.find("input").val('');
    }

    // Basic info make editable
    $("#province, #city, #country, #label, #genre").find('.editable').editable();

    //make status editable
    $('#status').editable({
        type: 'select',
        title: 'Select status',
        placement: 'right',
        value: 2,
        source: [
            {value: 1, text: 'status 1'},
            {value: 2, text: 'status 2'},
            {value: 3, text: 'status 3'}
            ],
        params: function(){ //ADD EXTRA PARAMETERS HERE!!
            //originally params contain pk, name and value
            params.a = 1;
            return params;
        }
        //uncomment these lines to send data on server
        ,pk: 1
        ,url: '/post'
    });


    var edit = false;
    // Enable Editing of Band Information and Performers
    $('#editpage').click(function(){
        if (edit) {
            $('#form').slideUp(400,clearPerformerForm);
            $('#addAlbum').fadeOut();
            $('#albumForm').slideUp();
            $('.performer-add').fadeOut();
            $('.song-add').fadeOut();
            $('.song-form').slideUp();
        }
        else{
            $('.performer-add').fadeIn();
            $('.song-add').fadeIn();
            $('#addAlbum').fadeIn();
        }
        $('.btn-mini').fadeToggle();
        $('.editable').editable('toggleDisabled');
        $(this).find('span').toggleClass('hide');
        edit = !edit;
    });


    // CRUD - PERFORMER
    $("#info").on('click', '.performer-delete',function () {
        // get the performer node
        var performer = $(this).closest("tr");
        var performerno = performer.data("performerno");

        // post to '/delete' in routes.py
        $.post("/delete", {
            band: $(".page-header").text(),
            performerno: performerno
        }, function () {
            // grab the siblings to renumber them later
            var tablerows = performer.siblings();

            // delete performer row
            performer.remove();

            // renumber the deleted performer's siblings
            for (var i = 0; i < tablerows.length; i++) {
                tablerows.eq(i).data("performerno", (i + 1));
            }
        });
    })
        // $('#info').
        .on("click", ".performer-add", function (){
            var table = $("#info").find("tbody");
            $("#form").slideDown();
            $(this).slideUp();
        })
        // $('#info').
        .on("click", ".performer-cancel", function (){
            $("#form").slideUp();
            $("#info").find('.performer-add').slideDown();
            clearPerformerForm();
        })
        // $('#info').
        .on("click", ".performer-submit", function(){
            var form = $("#form");
            var data = {
                    band : $(".page-header").text(),
                    instrument: form.find("select[name=instrument]").val(),
                    fullname: form.find("input[name=fullname]").val(),
                    joindate: form.find("input[name=joindate]").val()
                };
            var pNo = $('#info').find('tbody').children().length + 1 ; //adding 1 for increment
            var html =  $('<tr data-performerno="' +pNo+ '">\
                            <td class="perf-instrument">' +data.instrument+ '</td>\
                            <td class="perf-name">' +data.fullname+ '</td>\
                            <td class="perf-joindate">' +data.joindate+ '\
                            <a href="#!" class="performer-delete btn-mini pull-right"><i class="icon-remove"></i></a>\
                            </td>\
                        </tr>');

            $.post("/addperformer", data,
                function(response){
                    $('#info').find('tbody').append(html);
                    console.log(response);
                    clearPerformerForm();
                });

        });


    // CRUD - SONG
    $("#discography").on('click', '.song-delete',function () {
        // get the performer node
        var song = $(this).closest("tr");
        var songno = song.data("songno");

        // post to '/delete' in routes.py
        $.post("/deletesong", {
            band: $(".page-header").text(),
            album: $(song).closest('.album').data('title'),
            songno: $(this).closest('tr').data('songno'),
            somethingElse: "Trevor is awesome!!!!"}, function () {
            // grab the siblings to renumber them later
            var tablerows = song.siblings();

            // delete performer row
            song.remove();

            // renumber the deleted performer's siblings
            for (var i = 0; i < tablerows.length; i++) {
                tablerows.eq(i).data("songno", (i + 1));
            }
        });
    })
        // $('#discography').
        .on("click", ".song-add", function (){
            var album = $(this).closest(".album");
            album.find(".song-form").slideDown();
            $(this).slideUp();
        })
        // $('#info').
        .on("click", ".song-cancel", function (){
            var album = $(this).closest(".album");
            album.find(".song-form").slideUp();
            $("#discography").find('.song-add').slideDown();
            clearSongForm();
        })
        // $('#info').
        .on("click", ".song-submit", function(){
            var album = $(this).closest('.album');
            var songform = album.find('.song-form');
            var data = {
                    band : $(".page-header").text(),
                    album: album.data('title'),
                    songtitle: songform.find("input[name=songtitle]").val(),
                    duration: songform.find("input[name=duration]").val()
                };
            var sNo = album.find('tbody').children().length + 1 ; //adding 1 for increment
            var html =  $('<tr data-songno="'+sNo+'">\
                                <td>'+data.songtitle+'</td>\
                                <td>\
                                    '+data.duration+'\
                                    <a class="btn-mini pull-right song-delete"  href="#!"><i class="icon-remove"></i></a>\
                                </td>\
                            </tr>');

            $.post("/addsong", data,
                function(){
                    console.log("success");
                    console.log(this);
                    album.find('tbody').append(html);
                    clearSongForm();
                });

        }).on('click', '.album-delete', function(){
            album = $(this).closest('.album');
            title = album.data('title');
            if (confirm('Delete album "'+ title +'"?')){
                band = $(".page-header").text();
                data = {band: band, title: title}
                $.post('/deleteAlbum', data, function(){
                    album.fadeOut(album.remove);
                });
            }
        });


    $('#addAlbum').on('click', function(){
        var form = $('#albumForm');
        form.slideDown(function(){
            form.find('input[name=title]').focus();
        });
        $(this).slideUp();
    });

    $('#albumForm').on('click', '.album-cancel', function(){
        clearAlbumForm();
        $('#albumForm').slideUp();
        $('#addAlbum').slideDown();
    }).on('click', '.album-submit', function(){

            var form = $('#albumForm');
            var titleField = form.find("input[name=title]");
            var dateField = form.find("input[name=releaseDate]");
            var title = titleField.val();
            var date = dateField.val();

            console.log(title);
            if( title == '' || date == ''){
                return;
            }

            var band = $(".page-header").text();
            var data = {title:title, date:date, band:band}
            $.post("/addalbum", data, function(html){
                form.after($(html));
                form.next().slideDown();
            });
        });


    $('#addband').on('click', function(){
        $(this).hide();
        $('#submitband').show();
        $('#in').show('slide', {direction:'right'});
    });


});