package com.bao361.insurance.modules.main;

import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v4.app.FragmentTabHost;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

import com.bao361.insurance.R;
import com.bao361.insurance.base.BaseMvpActivity;
import com.bao361.insurance.modules.main.fragment.ClassFragmet;
import com.bao361.insurance.modules.main.fragment.FriendFragment;
import com.bao361.insurance.modules.main.fragment.QuestionFragment;
import com.bao361.insurance.modules.main.fragment.StaticsFragment;
import com.bao361.insurance.modules.main.presenter.MainPresenter;
import com.bao361.insurance.modules.main.viewimpl.MainView;

public class MainActivity extends BaseMvpActivity<MainPresenter> implements View.OnClickListener, MainView {

    private final static String TAG_QUESTION = "question";
    private final static String TAG_CLASS = "class";
    private final static String TAG_FRIEND = "friend";
    private final static String TAG_STATICS = "statics";


    private FragmentTabHost fragmentTabHost;
    private TextView questionTabView;
    private TextView classTabView;
    private TextView friendTabView;
    private TextView staticsTabView;

    private LayoutInflater inflater;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        inflater = LayoutInflater.from(this);


        initView();
    }

    private void initView() {
        initTab();

    }

    private void initTab() {

        fragmentTabHost = (FragmentTabHost) findViewById(android.R.id.tabhost);
        fragmentTabHost.setup(this, getSupportFragmentManager(), R.id.realtabcontent);
        //去掉分割线
        fragmentTabHost.getTabWidget().setDividerDrawable(null);

        //问吧
        View view = inflater.inflate(R.layout.main_tab_indicator, null);
        questionTabView = (TextView) view.findViewById(R.id.indication_name);
        questionTabView.setText(getString(R.string.tab_quesiton));
        Drawable questionDrawable = getResources().getDrawable(R.drawable.tab_question_selector);
        questionDrawable.setBounds(0, 0, questionDrawable.getIntrinsicWidth(), questionDrawable.getIntrinsicHeight());

        questionTabView.setCompoundDrawables(null, questionDrawable, null, null);

        fragmentTabHost.addTab(fragmentTabHost.newTabSpec(TAG_QUESTION).setIndicator(view), QuestionFragment.class, null);


        //课堂
        view = inflater.inflate(R.layout.main_tab_indicator, null);
        classTabView = (TextView) view.findViewById(R.id.indication_name);
        classTabView.setText(getString(R.string.tab_class));
        Drawable classDrawable = getResources().getDrawable(R.drawable.tab_question_selector);
        classDrawable.setBounds(0, 0, classDrawable.getIntrinsicWidth(), classDrawable.getIntrinsicHeight());
        classTabView.setCompoundDrawables(null, classDrawable, null, null);

        fragmentTabHost.addTab(fragmentTabHost.newTabSpec(TAG_CLASS).setIndicator(view), ClassFragmet.class, null);


        //朋友圈
        view = inflater.inflate(R.layout.main_tab_indicator, null);
        friendTabView = (TextView) view.findViewById(R.id.indication_name);
        friendTabView.setText(getString(R.string.tab_friend));
        Drawable friendDrawable = getResources().getDrawable(R.drawable.tab_question_selector);
        friendDrawable.setBounds(0, 0, friendDrawable.getIntrinsicWidth(), friendDrawable.getIntrinsicHeight());
        friendTabView.setCompoundDrawables(null, friendDrawable, null, null);

        fragmentTabHost.addTab(fragmentTabHost.newTabSpec(TAG_FRIEND).setIndicator(view), FriendFragment.class, null);

        //统计
        view = inflater.inflate(R.layout.main_tab_indicator, null);
        staticsTabView = (TextView) view.findViewById(R.id.indication_name);
        staticsTabView.setText(getString(R.string.tab_statics));
        Drawable staticsDrawable = getResources().getDrawable(R.drawable.tab_question_selector);
        staticsDrawable.setBounds(0, 0, staticsDrawable.getIntrinsicWidth(), staticsDrawable.getIntrinsicHeight());
        staticsTabView.setCompoundDrawables(null, staticsDrawable, null, null);

        fragmentTabHost.addTab(fragmentTabHost.newTabSpec(TAG_STATICS).setIndicator(view), StaticsFragment.class, null);

    }


    @Override
    public void onClick(View v) {


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
