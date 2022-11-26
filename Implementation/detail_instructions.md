Important: this whole file only supports 2020 version. We may read and follow step 1-6 to run the project 
(some modifications for .py files is done, so you can ignore them.)

You may store project path into a variable: (if not set)
- Enter:
  ```bash  
  echo "
  export SYSEVR_PATH=/home/SySeVR
  export WORKDIR=$SYSEVR_PATH/Implementation #/phase - varying dependent on working Phase
  export DATADIR=$SYSEVR_PATH/data" >> /etc/profile
  ```
- Save and run the file

### Phase 1 Generating Slices

> [WORK DIR] : /home/SySeVR/Implementation/source2slice (or $WORKDIR/source2slice)
>
> [DATA DIR] (also is working dir): /home/SySeVR/data (or $DATADIR)
>
> Recommended Memory Size: >=16GB (according to your code size)
>
> If you want to slice the NVD and SARD, you may divide them into parts.


1. parse the source code

   >input: source codes
   >
   >output: .joernIndex

   ```bash
   rm -rf $SYSEVR_PATH/data/.joernIndex #remove if existing
   ```

   ```bash
   # 4 is amount of RAM; you can change it to increase executing speed.
   # optional: NVD or SARD or each part of them; write to the end of line
   
   cd $SYSEVR_PATH/data
   java -Xmx4g -jar $JOERN_HOME/bin/joern.jar /home/SySeVR/data/source_data
   ```

   This will create a neo4j database directory .joernIndex in this directory.

2. generate CFG

   >input: .joernIndex
   >
   >output: cfg_db

    Prerequisite: set location of database with the 'org.neo4j.server.database.location' value 
    in /home/SySeVR/neo4j/conf/neo4j-server.properties 
    to match the .joernIndex's location.
	
   ```bash
   # start neo4j at other terminal
   /home/SySeVR/neo4j/bin/neo4j console
   ```

   ```bash
   rm -rf cfg_db # if existing
   mkdir cfg_db
   python2 $WORKDIR/source2slice/get_cfg_relation.py
   ```

3. generate PDG

   >input: cfg_db, .joernIndex
   >
   >output: pdg_db

   ```python
    # modify access_db_operate.py
    http.socket_timeout = 999999999 # a big number
   ```

   ```bash
   rm -rf pdg_db # if existing
   mkdir pdg_db
   python2 $WORKDIR/source2slice/complete_PDG.py
   ```

4. generate call graph of functions

   >input: pdg_db, .joernIndex
   >
   >output: dict_call2cfgNodeID_funcID

   ```bash
   rm -rf $DATADIR/dict_call2cfgNodeID_funcID # if existing
   mkdir $DATADIR/dict_call2cfgNodeID_funcID
   python2 $WORKDIR/source2slice/access_db_operate.py
   ```

5. generate four kinds of SyCVs

   >input: dict_call2cfgNodeID_funcID
   >
   >outout: arrayuse_slice_points.pkl, integeroverflow_slice_points_new.pkl, pointuse_slice_points.pkl, sensifun_slice_points.pkl

   ```python
    # modify points_get.py from the 122th row to the 130th
    # change "location" to ",location"
   
   ```

   ```bash
    python2 $WORKDIR/source2slice/points_get.py
   ```

6. extract slices

   >input: dict_call2cfgNodeID_funcID, arrayuse_slice_points.pkl, integeroverflow_slice_points_new.pkl, pointuse_slice_points.pkl, sensifun_slice_points.pkl
   >
   >output: api_slices.txt, arrayuse_slice.txt, integeroverflow_slices.txt, pointeruse_slice.txt

    ```bash
    rm -rf $DATADIR/slices # if existing
    mkdir $DATADIR/slices
    ```


   **Due to the limit of memory, you may execute four functions in extract_df.py one by one.**

   ```bash
   python2 $WORKDIR/source2slice/extract_df.py
   ```

7. get labels of slices

   >input: api_slices.txt, arrayuse_slice.txt, integeroverflow_slices.txt, pointeruse_slice.txt
   >
   >output: apt_slices_label.pkl, api_slices-vulline.pkl, array_slice_label.pkl, expr_slice_label.pkl, pointer_slice_label.pkl

   ```python
    # modify make_label.py at the 70th row
    # wrong format
   _dict_cwe2line = {}
   for _dict in dict:
      for key in _dict.keys():
         if _dict[key] not in _dict_cwe2line_target.keys():
   ```

   ```bash
   python2 make_label.py
   ```

8. combine labels with slices

   >input: apt_slices_label.pkl, api_slices-vulline.pkl, array_slice_label.pkl, expr_slice_label.pkl, pointer_slice_label.pkl, api_slices.txt, arrayuse_slice.txt, integeroverflow_slices.txt, pointeruse_slice.txt
   >
   >output: api_slices, arrayuse_slices.txt, integeroverflow_slices.txt, pointersuse_slices.txt

   ```bash
   # put files to specified folder in data_preprocess.py
   rm -rf $DATADIR/label_source $DATADIR/slice_label # if existing
   mkdir $DATADIR/label_source $DATADIR/slice_label
   mv apt_slices_label.pkl api_slices-vulline.pkl array_slice_label.pkl expr_slice_label.pkl pointer_slice_label.pkl ./label_source
   # rename
   cd label_source
   mv expr_slice_label.pkl integeroverflow_slices.pkl
   mv api_slices_label.pkl api_slices.pkl
   mv array_slice_label.pkl arrayuse_slice.pkl
   mv pointer_slice_label.pkl pointeruse_slice.pkl
   ```

   ```bash
   python2 data_preprocess.py
   ```
