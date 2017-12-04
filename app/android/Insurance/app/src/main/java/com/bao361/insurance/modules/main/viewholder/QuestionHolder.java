package com.bao361.insurance.modules.main.viewholder;

import android.content.Context;
import android.support.annotation.Nullable;
import android.support.v7.widget.RecyclerView;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.bao361.insurance.R;
import com.bao361.insurance.imageeagle.Eagle;
import com.bao361.insurance.imageeagle.EagleDiskCacheStrategy;
import com.bao361.insurance.modules.main.models.QuestionModel;
import com.bao361.insurance.ui.recycler.holders.ItemViewHolder;
import com.bao361.insurance.ui.widget.AutoLineLayout;

public class QuestionHolder extends ItemViewHolder<QuestionModel> {

    ImageView userImgView;
    TextView nameView;
    TextView dateView;
    TextView areaView;
    TextView questionView;
    TextView answerNumView;
    LinearLayout agentImgsLayout;


    public QuestionHolder(Context context, @Nullable RecyclerView parent) {
        super(context, parent, R.layout.question_item);
    }

    @Override
    protected void onBindViewHolder(int i, QuestionModel questionModel) {

        loadImage(questionModel.userImg, userImgView);

        nameView.setText(questionModel.name);
        dateView.setText(questionModel.date);
        areaView.setText(questionModel.area);
        questionView.setText(questionModel.question);
        answerNumView.setText(questionModel.answerNum + "个回答");

    }

    @Override
    protected void onItemClick(int i, QuestionModel questionModel) {


    }

    @Override
    protected void onViewCreated(View view) {
        userImgView = (ImageView) view.findViewById(R.id.userImg);
        nameView = (TextView) view.findViewById(R.id.name);
        dateView = (TextView) view.findViewById(R.id.date);
        areaView = (TextView) view.findViewById(R.id.area);
        questionView = (TextView) view.findViewById(R.id.question);
        agentImgsLayout = (LinearLayout) view.findViewById(R.id.agent_imgs);
        answerNumView = (TextView) view.findViewById(R.id.answer_num);

    }


    private void loadImage(String url, ImageView imageView) {
        Eagle.with(getContext())
                .load(url)
                .asBitmap()//只加载静态图片
                .placeholder(R.mipmap.default_img)
                .diskCacheStrategy(EagleDiskCacheStrategy.NONE)//缓存策略
                .error(R.mipmap.ic_launcher)//加载异常
                .into(imageView);


    }

}
