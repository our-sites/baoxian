package com.common.insurance.modules.main;

import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;

import com.common.insurance.R;
import com.common.insurance.base.BaseActivity;
import com.orhanobut.logger.Logger;

public class MainActivity extends BaseActivity<MainPresenter> implements View.OnClickListener, MainView {

    private ImageView imageView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        imageView = (ImageView) findViewById(R.id.image);
        findViewById(R.id.fengzhuangpost).setOnClickListener(this);
    }
    @Override
    public void onClick(View v) {

        Logger.d("message","ddd");

        switch (v.getId()) {
            case R.id.fengzhuangpost:
                loadImage();
                break;
        }

    }

    private void loadImage() {
        //支持加载gif图片
//        String url = "http://p1.pstatp.com/large/166200019850062839d3";
        String url = "http://cn.bing.com/az/hprichbg/rb/Dongdaemun_ZH-CN10736487148_1920x1080.jpg";
//        Glide.with(this)
//                .load(url)
//                .listener(new RequestListener<String, GlideDrawable>() {
//                    @Override
//                    public boolean onException(Exception e, String model, Target<GlideDrawable> target, boolean isFirstResource) {
//                        return false;
//                    }
//
//                    @Override
//                    public boolean onResourceReady(GlideDrawable resource, String model, Target<GlideDrawable> target, boolean isFromMemoryCache, boolean isFirstResource) {
//                        return false;
//                    }
//                })
////                .asBitmap()//只加载静态图片
////                .asGif()  //只加载动态图片，如果是静态图片，执行error
//                .placeholder(R.mipmap.ic_launcher)
//                .diskCacheStrategy(DiskCacheStrategy.NONE)//缓存策略
//                .error(R.mipmap.ic_launcher)//加载异常
//                .override(500, 500)//指定图片显示的宽高
//                .into(imageView);

//        Eagle.with(this)
//                .load(url)
//                .asBitmap()//只加载静态图片
////                .asGif()  //只加载动态图片，如果是静态图片，执行error
//                .placeholder(R.mipmap.ic_launcher)
//                .diskCacheStrategy(EagleDiskCacheStrategy.NONE)//缓存策略
//                .error(R.mipmap.ic_launcher)//加载异常
//                .size(500, 500)//指定图片显示的宽高
//                .into(imageView);


    }


    private void sendRequest() {
        getPresenter().sendEncapsulationPost();
    }

    @Override
    protected MainPresenter createPresenter() {
        return new MainPresenter();
    }


    @Override
    public void setLoadingIndicator(boolean active) {

    }

    @Override
    public boolean refresh() {
        return false;
    }


    @Override
    public void setText() {

    }
}
