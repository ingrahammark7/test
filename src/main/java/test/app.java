package test;

import test.util.importdata;
import test.util.util;

public class app {

  public static void main(String[] args) throws Exception {
    // util.getpos();
    dof();
  }

  public static void dof() throws Exception {
    importdata.importing();
    util.iterate();
  }



}
