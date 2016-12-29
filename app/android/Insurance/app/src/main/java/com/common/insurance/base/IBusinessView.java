package com.common.insurance.base;


public interface IBusinessView extends IView {

    void setLoadingIndicator(boolean active);

    boolean refresh();


}
