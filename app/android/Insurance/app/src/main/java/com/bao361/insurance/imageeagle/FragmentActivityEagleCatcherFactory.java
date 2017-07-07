package com.bao361.insurance.imageeagle;


import android.support.v4.app.FragmentActivity;

/**
 * 创建Fragment类型的图片获取器
 */
public class FragmentActivityEagleCatcherFactory extends AbstractEagleCatcherFactory<FragmentActivity> {


    @Override
    public ICatcher createEagleCatcher(FragmentActivity fragmentActivity) {
        ICatcher iCatcher = new EagleCatcher(fragmentActivity);
        return iCatcher;
    }
}
