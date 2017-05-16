package com.common.insurance.imageeagle;


import android.app.Fragment;

/**
 * 创建Fragment类型的图片获取器
 */
public class AppFragmentEagleCatcherFactory extends AbstractEagleCatcherFactory<Fragment> {


    @Override
    public ICatcher createEagleCatcher(Fragment fragment) {
        ICatcher iCatcher = new EagleCatcher(fragment);
        return iCatcher;
    }
}
