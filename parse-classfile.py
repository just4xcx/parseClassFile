# -*- coding: utf-8 -*-
import struct
import codecs

'''
ClassFile {
    u4             magic;
    u2             minor_version;
    u2             major_version;
    u2             constant_pool_count;
    cp_info        constant_pool[constant_pool_count-1];
    u2             access_flags;
    u2             this_class;
    u2             super_class;
    u2             interfaces_count;
    u2             interfaces[interfaces_count];
    u2             fields_count;
    field_info     fields[fields_count];
    u2             methods_count;
    method_info    methods[methods_count];
    u2             attributes_count;
    attribute_info attributes[attributes_count];
}


cp_info {
    u1 tag;
    u1 info[];
}

Constant Type 	            Value
CONSTANT_Class 	            7
CONSTANT_Fieldref 	    9
CONSTANT_Methodref 	    10
CONSTANT_InterfaceMethodref 	11
CONSTANT_String 	8
CONSTANT_Integer 	3
CONSTANT_Float 	        4
CONSTANT_Long 	        5
CONSTANT_Double 	6
CONSTANT_NameAndType 	12
CONSTANT_Utf8 	        1
CONSTANT_MethodHandle 	15
CONSTANT_MethodType 	16
CONSTANT_InvokeDynamic 	18


       

CONSTANT_Class_info {
    u1 tag;
    u2 name_index;
}


CONSTANT_Fieldref_info {
    u1 tag;
    u2 class_index;
    u2 name_and_type_index;
}

CONSTANT_Methodref_info {
    u1 tag;
    u2 class_index;
    u2 name_and_type_index;
}

CONSTANT_InterfaceMethodref_info {
    u1 tag;
    u2 class_index;
    u2 name_and_type_index;
}

CONSTANT_String_info {
    u1 tag;
    u2 string_index;
}

CONSTANT_Integer_info {
    u1 tag;
    u4 bytes;
}

CONSTANT_Float_info {
    u1 tag;
    u4 bytes;
}

CONSTANT_Long_info {
    u1 tag;
    u4 high_bytes;
    u4 low_bytes;
}

CONSTANT_Double_info {
    u1 tag;
    u4 high_bytes;
    u4 low_bytes;
}

CONSTANT_NameAndType_info {
    u1 tag;
    u2 name_index;
    u2 descriptor_index;
}

CONSTANT_Utf8_info {
    u1 tag;
    u2 length;
    u1 bytes[length];
}

CONSTANT_MethodHandle_info {
    u1 tag;
    u1 reference_kind;
    u2 reference_index;
}

CONSTANT_MethodType_info {
    u1 tag;
    u2 descriptor_index;
}

CONSTANT_InvokeDynamic_info {
    u1 tag;
    u2 bootstrap_method_attr_index;
    u2 name_and_type_index;
}


'''


tags = {
        7: {'name': 'Class', 'size': 2},
        9: {'name': 'Fieldref', 'size': 4},
        10: {'name': 'Methodref', 'size': 4},
        11: {'name': 'InterfaceMethodref', 'size': 4},
        8: {'name': 'String', 'size': 2},
        3: {'name': 'Integer', 'size': 4},
        4: {'name': 'Float', 'size': 4},
        5: {'name': 'Long', 'size': 8},
        6: {'name': 'Double', 'size': 8},
        12: {'name': 'NameAndType', 'size': 4},
        #1: {'name': 'Utf8', 'size': 2},
        15: {'name': 'MethodHandle', 'size': 3},
        16: {'name': 'MethodType', 'size': 2},
        18: {'name': 'InvokeDynamic', 'size': 4},
    }


def process_pools(f, pool_cnt):
    
    print 'pool count:' + str(pool_cnt)
    cur_pool = 1
    str_cnt = 0
    contain_slash_strs = []
    while cur_pool < pool_cnt :
        tag = f.read(1)
        tag = struct.unpack('B', tag)[0]
        #print 'tag ->' + str(tag)
        if tag == 1 :
            str_cnt += 1
            str_len = struct.unpack('>H', f.read(2))[0]
            str_content = f.read(str_len)
            str_content = codecs.decode(str_content, 'utf-8')
            #print 'str_content ->' + str_content
            if str_content.find('\\') >= 0:
                #print str_content
                contain_slash_strs.append(str_content)           
        else:
            f.read(tags[tag]['size'])
        cur_pool += 1

    print '一共有常量字符串', str_cnt, '个'
    print '包含"\\"的有如下：'
    for s in contain_slash_strs:
        print '\t', s
        
def process_file(file_name):
    print '开始扫描文件：', file_name
    with open(file_name, "rb") as f:
        magicHdr = f.read(4)
        magicHdr = struct.unpack('>I', magicHdr)[0]
        #0xcafebabe
        #print struct.unpack('>I', magicHdr)[0]
        #print 0xcafebabe
        if 0xcafebabe != magicHdr:
            print '不是有效的Java ClassFile文件！'
        else:
            vers = f.read(4)
            print 'version:' + str(struct.unpack('>2H', vers))
            pool_cnt = f.read(2)
            pool_cnt = struct.unpack('>H', pool_cnt)[0]
            process_pools(f, pool_cnt)
            
                    
            f.close()

        
    #while byte != "":
    #    # Do stuff with byte.
    #    byte = f.read(1)

process_file("DepateNumCount.class")








    
