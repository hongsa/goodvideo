(function ($, undefined) {
    'use strict';

    var OFFSET = 6;

    $.fn.rating = function (options) {
        this.each(function () {
            var $input = $(this);
            // Merge data and parameter options.
            // Those provided as parameter prevail over the data ones.
            var opts = $.extend({}, $input.data(), options);
            // Sanitize start, stop, and step.
            // All of them start, stop, and step must be integers.
            // In case we don't have a valid stop rate try to get a reasonable
            // one based on the existence of a valid start rate.
            opts.start = parseInt(opts.start, 10) || undefined;
            opts.stop = parseInt(opts.stop, 10) ||
            opts.start + OFFSET ||
            undefined;
            opts.step = parseInt(opts.step, 10) || undefined;

            // Extend/Override the default options with those provided either as
            // data attributes or function parameters.
            opts = $.extend({}, $.fn.rating.defaults, opts);

            // Fill rating symbols until index.
            var fillUntil = function (index) {
                var $rates = $rating.children();
                // Empty all just in case index is NaN.
                $rates.removeClass(opts.filled).addClass(opts.empty);
                // Fill all the symbols up to the selected one.
                $rates.eq(index).prevAll('.rating-symbol').addBack()
                    .removeClass(opts.empty).addClass(opts.filled);
            };

            // Calculate the rate of an index according the the start and step.
            var indexToRate = function (index) {
                return opts.start + index * opts.step;
            };

            // Get the corresponding index of a rate or NaN if rate is not a number.
            var rateToIndex = function (rate) {
                return Math.max(Math.ceil((rate - opts.start) / opts.step), 0);
            };

            // Check the rate is in the proper range [start..stop) and with
            // the proper step.
            var contains = function (rate) {
                var start = opts.step > 0 ? opts.start : opts.stop;
                var stop = opts.step > 0 ? opts.stop - 1 : opts.start + 1;
                return start <= rate && rate <= stop && (opts.start + rate) % opts.step === 0;
            };

            // Update empty and filled rating symbols according to a rate.
            var updateRate = function (rate) {
                var value = parseInt(rate, 10);
                if (contains(value)) {
                    fillUntil(rateToIndex(value));
                }
            };

            // Call f only if the input is enabled.
            var ifEnabled = function (f) {
                return function () {
                    if (!$input.prop('disabled') && !$input.prop('readonly')) {
                        f.call(this);
                    }
                }
            };

            // Build the rating control.
            var $rating = $('<div></div>').insertBefore($input);
            for (var i = 0; i < rateToIndex(opts.stop); i++) {
                var $symbol = $('<div class="rating-symbol ' + opts.empty + '"></div>');
                $rating.append($symbol);
                opts.extendSymbol.call($symbol, indexToRate(i));
            }
            // Initialize the rating control with the associated input value rate.
            updateRate($input.val());

            // Keep rating control and its associated input in sync.
            $input
                .on('change', function () {
                    updateRate($(this).val());
                });

            $rating
                .on('click', '.rating-symbol', ifEnabled(function () {
                    // Set input to the current value and 'trigger' the change handler.
                    $input.val(indexToRate($(this).index())).change();
                }))
                .on('mouseenter', '.rating-symbol', ifEnabled(function () {
                    // Emphasize on hover in.
                    fillUntil($(this).index());
                }))
                .on('mouseleave', '.rating-symbol', ifEnabled(function () {
                    // Restore on hover out.
                    fillUntil(rateToIndex(parseInt($input.val(), 10)));
                }));
        });
    };

    // Plugin defaults.
    $.fn.rating.defaults = {
        filled: 'glyphicon glyphicon-star',
        empty: 'glyphicon glyphicon-star-empty',
        start: 1,
        stop: OFFSET,
        step: 1,
        extendSymbol: function (rate) {},
    };

    $(function () {
        $('input.rating').rating();
    });
}(jQuery));

toastr.options = {
    "closeButton": false,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-center",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "1500",
    "extendedTimeOut": "1500",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
};

$(document).ready(function(){

    $("#actor_rank").click(function(){
        // alert("rate");
        $(".actor_show_rank").show();
        $(".actor_show_click").hide();
    });

    $("#actor_click").click(function(){
        $(".actor_show_rank").hide();
        $(".actor_show_click").show();
    });

    $("#video_rank").click(function(){
        // alert("rate");
        $(".video_show_rank").show();
        $(".video_show_click").hide();
    });

    $("#video_click").click(function(){
        $(".video_show_rank").hide();
        $(".video_show_click").show();
    });

    $('.v_star_area').find('input').rating({
        extendSymbol: function (rate) {
            $(this).tooltip({
                container: 'body',
                placement: 'top',
                title: '평점 ' + rate+ "점!"
            });
        }
    });

    //$('.v_star_area').find('input').on('change', function () {
    //    alert($(this).val()+'점 평가 완료!!');
    //});

    $('.v_star_area').find('input').on('change', function () {
        $.ajax({
            url: '/v_save_star',
            type: 'POST',
            dataType: 'JSON',
            data:{
                name: $(this).parent().parent().attr('id'),
                star: this.value
            },
            success: function(data) {
                if(data.success){

                    Command: toastr["success"]("평가완료되었습니다!");
                }
                else{
                    alert("error");
                }
            }
        });
    });


    $('.a_star_area').find('input').rating({
        extendSymbol: function (rate) {
            $(this).tooltip({
                container: 'body',
                placement: 'top',
                title: '평점 ' + rate+ "점!"
            });
        }
    });


    //$('.a_star_area').find('input').on('change', function () {
    //    alert($(this).val()+'점 평가 완료!!');
    //});

    $('.a_star_area').find('input').on('change', function () {
        $.ajax({
            url: '/a_save_star',
            type: 'POST',
            dataType: 'JSON',
            data:{
                name: $(this).parent().parent().attr('id'),
                star: this.value
            },
            success: function(data) {
                if(data.success){

                    Command: toastr["success"]("평가완료되었습니다!");


                    //alert('소신있는 나의 평가완료!!');
                }
                else{
                    alert("error");
                }
            }
        });
    });


    $('.v_bookmark').click(function () {
        $.ajax({
            url: '/v_bookmark',
            type: 'POST',
            dataType: 'JSON',
            data:{
                name: $(this).parent().parent().attr('id')
            },
            success: function(data) {
                if(data.success){

                    Command: toastr["success"]("영상컬렉션에 저장되었습니다!");
                }
                else{
                    alert("error");
                }
            }
        });
    });




    $('.a_bookmark').click(function () {
        $.ajax({
            url: '/a_bookmark',
            type: 'POST',
            dataType: 'JSON',
            data:{
                name: $(this).parent().parent().attr('id')
            },
            success: function(data) {
                if(data.success){

                    Command: toastr["success"]("배우컬렉션에 저장되었습니다!");
                }
                else{
                    alert("error");
                }
            }
        });
    });




});
