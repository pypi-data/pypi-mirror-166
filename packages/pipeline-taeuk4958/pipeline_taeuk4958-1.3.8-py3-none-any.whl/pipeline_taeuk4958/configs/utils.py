
import os
from pipeline_taeuk4958.configs.config import Config

def change_to_tuple(cfg, boolean_flag):
    if isinstance(boolean_flag, dict):
        assert isinstance(cfg, dict), isinstance(boolean_flag, dict)
            
        for key in list(cfg.keys()):
            cfg[key] = change_to_tuple(cfg[key], boolean_flag[key])
    elif isinstance(boolean_flag, list):
        assert isinstance(cfg, list), isinstance(boolean_flag, list)
            
        for idx in range(len(cfg)):
            cfg[idx] = change_to_tuple(cfg[idx], boolean_flag[idx])
    
    elif boolean_flag == True:
        return tuple(cfg)
            
        
    return cfg  




def load_config(cfg_dict):
    cfg = change_to_tuple(cfg_dict['cfg_dict'], cfg_dict['tuple_flag'])
    
    config_file_path = os.path.join(os.getcwd(), cfg_dict['cfg_name'])  
    with open(config_file_path, 'w') as f:
        f.write('\n')       # 빈 file 생성
    
    return Config.fromfile(config_file_path, cfg)       # 빈 file에 config를 그대로 옮겨쓴다.
    
    
    
    

def load_config_in_pipeline(cfg_path):
    if not cfg_path.endswith('.py'):
        cfg_pyformat_path = cfg_path + ".py"        # cfg_pyformat_path : {wiorkspace}/inputs/cfg/data.py
                                                    # can't command 'mv' 
    
    # change format to .py
    with open(cfg_path, "r") as f:
        data = f.read()
    with open(cfg_pyformat_path, "w") as f:
        f.write(data)       
    f.close()
    
    return Config.fromfile(cfg_pyformat_path)       # cfg_pyformat_path : must be .py format  