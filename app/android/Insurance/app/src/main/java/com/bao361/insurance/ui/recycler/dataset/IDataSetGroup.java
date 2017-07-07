package com.bao361.insurance.ui.recycler.dataset;

import java.util.List;


public interface IDataSetGroup<Group, Child> {

    public static class Index {
        public final int groupIndex;
        public final int childIndex;

        public Index(int groupIndex, int childIndex) {
            this.groupIndex = groupIndex;
            this.childIndex = childIndex;
        }
    }

    public int size();

    public int sizeOfGroup();

    public int sizeOfChild(int groupIndex);

    /**
     * 查找 group index,
     *
     * @param position list position.
     * @return group index.
     */
    public int turnGroupIndex(int position);

    /**
     * 查找position的group position
     *
     * @param position any list position
     * @return
     */
    public int getGroupPosition(int position);

    /**
     * 查找 child index,
     *
     * @param position list position.
     * @return child index.
     */
    public Index turnChildIndex(int position);

    public boolean isGroup(int position);

    public void setDataSet(List<Group> groups, List<List<Child>> childs);

    public void addGroup(Group group, List<Child> childs);

    public void addChilds(Group group, List<Child> childs);

    public void addChilds(int groupIndex, List<Child> childs);

    public void setChilds(int groupIndex, List<Child> childs);

    public void setChilds(Group group, List<Child> childs);

    public void addChild(Group group, Child child);

    public void addChild(int groupIndex, Child child);

    public int indexOf(Group group);

    public Group getGroup(int groupIndex);

    public List<Group> getGroups();

    public Child getChild(int groupIndex, int childIndex);

    public List<Child> getChilds(int groupIndex);

//    public List<List<Child>> getChilds();

    public void removeGroup(int groupIndex);

    public void removeChild(int groupIndex, int childIndex);

    public void clear();

    public boolean isEmpty();

    public boolean isEmptyChilds(int groupIndex);

    public void clearChilds(int groupIndex);
}
