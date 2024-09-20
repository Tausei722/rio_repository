document.addEventListener('DOMContentLoaded', () => {
// ナビゲートバーの呼び出しのスイッチ機能
const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

// Check if there are any navbar burgers
if ($navbarBurgers.length > 0) {
    // Add a click event on each of them
    $navbarBurgers.forEach( el => {
    el.addEventListener('click', () => {
        const target = document.getElementById(el.dataset.target);
        target.classList.toggle('is-active');
    });
    });
}

// // ここでログイン、サインイン失敗のメッセージの表示をスイッチで代用
// const button = document.getElementById("myButton")
// const hyde = document.getElementById("hyde")
// button.addEventListener("click", function() {
//     // テキストを表示する
//     hyde.classList.remove('hyde');
//     // 今の状態をlocalStrageに保存
//     localStorage.setItem('textDeleted', 'false');
//   });
//   //ページ読み込み時にローカルストレージのデータを読み込む
//   window.onload = () => {
//     const isTextDeleted = localStorage.getItem('textDeleted');
//     if (isTextDeleted == 'false'){
//         document.getElementById("hyde").classList.remove('hyde');
//     }
//   }
//   //ページを離れるときにメッセージ削除を停止する
//   const targetUrl = 'http://127.0.0.1:8000/flash/signin';
//   const currentUrl = window.location.href;
//   window.onload = () => {
//     if (currentUrl === targetUrl){
//         hyde.classList.add('hyde');
//     }else{
//         hyde.classList.add('hyde'); 
//     }
//   }

// //ajaxを使えるようにするためのおまじない
// function getCookie(name) {
//   var cookieValue = null;
//   if (document.cookie && document.cookie !== '') {
//       var cookies = document.cookie.split(';');
//       for (var i = 0; i < cookies.length; i++) {
//           var cookie = jQuery.trim(cookies[i]);
//           // Does this cookie string begin with the name we want?
//           if (cookie.substring(0, name.length + 1) === (name + '=')) {
//               cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//               break;
//           }
//       }
//   }
//   return cookieValue;
// }

// var csrftoken = getCookie('csrftoken');

// function csrfSafeMethod(method) {
//   // these HTTP methods do not require CSRF protection
//   return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
// }

// $.ajaxSetup({
//   beforeSend: function (xhr, settings) {
//       if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
//           xhr.setRequestHeader("X-CSRFToken", csrftoken);
//       }
//   }
// });

  // var csrfToken = "{{ csrf_token }}";
  // const loading = document.getElementById('loading')
  // // 非同期処理をする宣言
  // $.ajax({
  //   url: "",
  //   type: 'POST',
  //   headers: {
  //     'X-CSRFToken': csrfToken
  //   },
  // })
  // .done(function(response){
  //   loading.classList.remove('loading');
  // })
  // .fail(function(error){
  //   alert(error);
  //   console.log(error);
  // })
  // .always(function(response){
  //   loading.classList.add('loading');
  // });

  //どこのフォームのことかを指定
  const form = document.forms.movie
  const formInput = document.forms.movie.elements.movie
  const loader = document.getElementById("loading");
  const loadButton = form.querySelector('.button');

  // Inputタグに値がセットされたら行える
  formInput.addEventListener('change', () => {
    //ボタンが押されたらロード画面表示
    loadButton.addEventListener('click', function() {
      loader.classList.remove('loading');
      console.log('a');
    }, false)
      // 処理が始まった時(POSTを受け取り)ロード画面を表示
      .done(function(){
        console.log(data);
        loading.classList.remove('loading');
        alert('５分ほどかかる場合があります');
      })
      .fail(function(error){
        console.log(data);
        alert('失敗しました');
      })
      // 処理完了時にローディングを消す
      .always(function(){
        console.log(data);
        loading.classList.add('loading');
      });
      }
    );
  
});
