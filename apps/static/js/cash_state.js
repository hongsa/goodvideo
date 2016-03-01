/* 서버쪽으로 데이터를 보내보자 */
$(document).ready(function(){
    $('.btn_state').click(function(){
        /* 일단 처리할 정보를 가져오자. ( jquery 이용 ) */
        var state = $(this).val();


        $.ajax({
            url: '/state', // 데이터 보낼 주소.
            type: 'POST',
            dataType: 'JSON',
            data: {
                id: $(this).parent().attr('id'),
                value: state
            },
            method: 'POST', // 포스트로 보내기로했지?
            success: function(data) {
                if(data.success){

                    alert('처리되었습니다.');
                }
                else{
                    alert("error");
                }
            }
        });
    });

});