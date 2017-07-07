package com.bao361.insurance.base;


public interface IBusinessView extends IView {

    void setLoadingIndicator(boolean active);

    boolean refresh();


}
