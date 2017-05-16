package com.common.insurance.imageeagle;

import android.support.v4.app.Fragment;

/**
 * 创建Fragment类型的图片获取器
 */
public class SupportFragmentEagleCatcherFactory extends AbstractEagleCatcherFactory<Fragment> {


    @Override
    public ICatcher createEagleCatcher(Fragment fragment) {
        ICatcher iCatcher = new EagleCatcher(fragment);
        return iCatcher;
    }
}
