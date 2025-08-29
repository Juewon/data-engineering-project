$(document).ready(function(){
    $('#guSearchForm').on('submit', function(event){
        // submit 이벤트 기본 기능 : 페이지 새로고침
        // 페이지 새로고침 되지 않도록
        event.preventDefault();  

        let formData = $(this).serialize();
        console.log(formData)

        $.ajax({
            type:"post",
            url:"http://127.0.0.1:8000/deep_app/show_res_map/",
            data:formData,
            datatype:'json',
            success:function(result){
                console.log(result)
                $('#searchResultBox').html(result) // #searchResultBox id 태그내에 html 코드를 삽입하는 함수(코드는 result에서 반환받음)
            },
            error:function(){
                // 오류 발생 시 수행되는 함수
                alert("오류 발생")
            },
            complete:function(){
                // 완료 되었을 때 수행되는 함수
            }
        });
    })

});