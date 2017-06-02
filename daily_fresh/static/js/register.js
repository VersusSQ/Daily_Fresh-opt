$(function(){
	// 用来标记每个字段的校验是否正确
	// true表示默认字段信息为不符合条件的
	var error_name = true;
	var error_password = true;
	var error_check_password = true;
	var error_email = true;
	// 用来标记勾选的,默认false表示,前台显示为勾选的
	var error_check = false;

	//　当id为user_name的标签失去焦点时，执行函数check_user_name()
	$('#user_name').blur(function() {
		check_user_name();
	});

	$('#pwd').blur(function() {
		check_pwd();
	});

	$('#cpwd').blur(function() {
		check_cpwd();
	});

	$('#email').blur(function() {
		check_email();
	});

	$('#allow').click(function() {
		// 判断当前是否处于被选中状态
		if($(this).is(':checked'))
		{
			error_check = false;
			// 同级的span标签
			$(this).siblings('span').hide();
		}
		else
		{
			error_check = true;
			$(this).siblings('span').html('请勾选同意');
			$(this).siblings('span').show();
		}
	});

	function check_user_name(){
		// val()获取当前表单input标签的值
		var len = $('#user_name').val().length;
		if(len<5||len>20)
		{
			$('#user_name').next().html('请输入5-20个字符的用户名');
			$('#user_name').next().show();
			error_name = true;
		}
		else
		{
            $('#user_name').next().hide();
			// ajax发送http请求,自动发送,在后端views处判断，该用户名是否存在,返回查找数据库的结果
			$.get('/register_exist/?uname='+$('#user_name').val(),function (data) {
				if(data.count==1){
					$('#user_name').next().html('用户名已经存在')
					$('#user_name').next().show();
					error_name = true;
				}else{
					$('#user_name').next().hide();
                	error_name = false;
				}
            });
		}
	}

	function check_pwd(){
		var len = $('#pwd').val().length;
		if(len<8||len>20)
		{
			$('#pwd').next().html('密码最少8位，最长20位')
			$('#pwd').next().show();
			error_password = true;
		}
		else
		{
			$('#pwd').next().hide();
			error_password = false;
		}		
	}

	function check_cpwd(){
		var pass = $('#pwd').val();
		var cpass = $('#cpwd').val();

		if(pass!=cpass)
		{
			$('#cpwd').next().html('两次输入的密码不一致')
			$('#cpwd').next().show();
			error_check_password = true;
		}
		else
		{
			$('#cpwd').next().hide();
			error_check_password = false;
		}		
		
	}

	function check_email(){
		var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;

		if(re.test($('#email').val()))
		{
			$('#email').next().hide();
			error_email = false;
		}
		else
		{
			$('#email').next().html('你输入的邮箱格式不正确');
			$('#email').next().show();
			error_check_password = true;
		}

	}

	// submit(),表示出发submit事件触发的函数
	$('#reg_form').submit(function() {

		check_user_name();
		check_pwd();
		check_cpwd();
		check_email();

		if(error_name == false && error_password == false && error_check_password == false && error_email == false && error_check == false)
		{
			return true;
		}
		else
		{
			return false;
		}

	});

});