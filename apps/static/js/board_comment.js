/* 서버쪽으로 데이터를 보내보자 */
$(document).ready(function(){
    $('#board_comment').click(function(){
        /* 일단 처리할 정보를 가져오자. ( jquery 이용 ) */
        var inputComment = $('input[name=comment]').val();
        var inputBoardId = $('input[name=board_id]').val();

        if ((inputComment=="")|| inputComment==null){
            alert("내용을 입력해주세요!");
            return;
        }

        if ((inputComment.indexOf("<")!=-1) ||(inputComment.indexOf(">")!=-1) || (inputComment.indexOf("$")!=-1)
            ||(inputComment.indexOf("#")!=-1) ||(inputComment.indexOf("{")!=-1)||(inputComment.indexOf("}")!=-1)
            ||(inputComment.indexOf("[")!=-1)||(inputComment.indexOf("]")!=-1)||(inputComment.indexOf("/")!=-1))
        {
            alert("특수문자는 사용할 수 없습니다!");
            return;
        }

        $('input[type="text"],textarea').val('');
        var $target = $('html,body');
        $target.animate({scrollTop: $(document).height()-$(window).height()}, 300);

        /* 보낼 데이터 객체로 준비 ( 이게 제일 심플함. )
         서버에서는 input 이라는 이름으로 데이터를 받기로 약속되어져있다. AjaxSample.py 참고 */
        var sParam = {
            comment: inputComment,
            id: inputBoardId
        }
        /* 보내보자 시바 */
        $.ajax({
            url: '/answer', // 데이터 보낼 주소.
            data: sParam, // 데이터 보낼것 ( key = value 쌍 구조를 이루고있어야됨 )
            dataType: "JSON",
            method: 'POST', // 포스트로 보내기로했지?
            success: receiverHandler, // 핸들러 등록 아래 참고.
            error: errorHandler //
        });
    });
    $('#board_input').keypress(function(e){
        if(e.which == 13){
            $('#board_comment').click();
        }
    });
});
/* 서버에서 계산한 결과가 왔을때 처리할 부분 */
var receiverHandler = function(result, textStatus, xhr) {
    $
    $('#current').before('<div class="panel panel-default">'+'<div class="row">'+'<div class="col-sm-2 text-left">'+'<p class="comment_author">'+'&nbsp;&nbsp;'+result['partner']+'</p>'+'</div>'+'<div class="col-sm-9">'+'<p class="text-center commentBox">' +result['comments']+'</p>'+'</div>'+'</div>'+'</div>');
    alert('저장완료')

};

var errorHandler = function(){
    alert('error')
}/**
 * Created by hongsasung on 15. 2. 18..
 */
