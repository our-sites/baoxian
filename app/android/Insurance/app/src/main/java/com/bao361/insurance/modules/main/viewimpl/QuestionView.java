package com.bao361.insurance.modules.main.viewimpl;

import com.bao361.insurance.base.IBusinessView;
import com.bao361.insurance.modules.main.models.QuestionModel;

import java.util.ArrayList;

public interface QuestionView extends IBusinessView {

    void setData(ArrayList<QuestionModel> models);
}
