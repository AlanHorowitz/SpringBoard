## Hadoop Mini Project

### Run two streaming map reduce jobs in Hortonworks sandbox

### Demonstration instructions

- Install HortonWorks HDP Sandbox 3.0 as a VirtualBox appliance
- Create admin user and /user/admin/input folder
- Update admin and input folders to full write permissions 
- Log into sandbox terminal as root
- git clone https://github.com/AlanHorowitz/SpringBoard.git
- cd hadoop-mini-project
- hadoop fs -put data.csv /user/admin/input
- ./hadoop_mr.sh > hadoop_mr.out >2&1

### Results

- Output of successful map reduce jobs at /user/admin/make_year_count
- Output log at hadoop.mr_out
