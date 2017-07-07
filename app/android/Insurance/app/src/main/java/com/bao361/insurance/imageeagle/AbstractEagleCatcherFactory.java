package com.bao361.insurance.imageeagle;

/**
 *
 */
public abstract class AbstractEagleCatcherFactory<T> {

    public abstract ICatcher createEagleCatcher(T t);

}
