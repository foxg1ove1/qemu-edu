import os

# toolchains options
ARCH        ='risc-v'
CPU         ='virt64'
CROSS_TOOL  ='gcc'

RTT_ROOT = os.getenv('RTT_ROOT') or os.path.join(os.getcwd(), '..', '..', 'rt-thread')

if os.getenv('RTT_CC'):
    CROSS_TOOL = os.getenv('RTT_CC')

if  CROSS_TOOL == 'gcc':
    PLATFORM    = 'gcc'
    EXEC_PATH   = os.getenv('RTT_EXEC_PATH') or '/usr/bin'
else:
    print('Please make sure your toolchains is GNU GCC!')
    exit(0)

BUILD = 'debug'

if PLATFORM == 'gcc':
    # toolchains
    PREFIX  = os.getenv('RTT_CC_PREFIX') or 'riscv64-unknown-elf-'
    CC      = PREFIX + 'gcc'
    CXX     = PREFIX + 'g++'
    AS      = PREFIX + 'gcc'
    AR      = PREFIX + 'ar'
    LINK    = PREFIX + 'gcc'
    TARGET_EXT = 'elf'
    SIZE    = PREFIX + 'size'
    OBJDUMP = PREFIX + 'objdump'
    OBJCPY  = PREFIX + 'objcopy'
    STRIP   = PREFIX + 'strip'

    DEVICE  = ' -mcmodel=medany -march=rv64imafdc -mabi=lp64 '
    CFLAGS  = DEVICE + '-ffreestanding -flax-vector-conversions -Wno-cpp -fno-common -ffunction-sections -fdata-sections -fstrict-volatile-bitfields -fdiagnostics-color=always'
    AFLAGS  = ' -c' + DEVICE + ' -x assembler-with-cpp -D__ASSEMBLY__ '
    LFLAGS  = DEVICE + ' -nostartfiles -Wl,--gc-sections,-Map=rtthread.map,-cref,-u,_start -T link.lds' + ' -lsupc++ -lgcc -static'
    CPATH   = ''
    LPATH   = ''

    if BUILD == 'debug':
        CFLAGS += ' -O0 -ggdb -fvar-tracking '
        AFLAGS += ' -ggdb'
    else:
        CFLAGS += ' -O2 -Os'

    CXXFLAGS = CFLAGS
    # Module support
    M_CFLAGS = CFLAGS + ' -fPIC --align-sections=8'
    M_CXXFLAGS = CXXFLAGS + ' -fPIC --align-sections=8'
    M_LFLAGS = DEVICE + ' -shared -fPIC -nostartfiles -Wl,--gc-sections --align-sections=8'
    M_CFLAGS = CFLAGS + ' -mlong-calls -fPIC'
    M_CXXFLAGS = CXXFLAGS + ' -mlong-calls -fPIC'
    M_LFLAGS = DEVICE + CXXFLAGS + ' -Wl,--gc-sections,-z,max-page-size=0x4' +\
                                ' -shared -fPIC -nostartfiles -nostdlib -static-libgcc'

    # Post actions
M_POST_ACTION = STRIP + ' -R .hash $TARGET\n' + SIZE + ' $TARGET \n'
M_BIN_PATH = '/home/fox/OSPP/RT-Thread/qemu-edu/machines/qemu-virt-riscv64/fat'
DUMP_ACTION = OBJDUMP + ' -D -S $TARGET > rtthread.asm\n'
POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' + SIZE + ' $TARGET \n'
