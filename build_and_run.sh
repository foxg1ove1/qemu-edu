#!/bin/bash
# filepath: /home/fox/OSPP/riscv_rtt_rust/build_and_run.sh

set -e

WORKDIR="/home/fox/OSPP/RT-Thread/qemu-edu"
RUSTAPP="$WORKDIR/rt-thread/components/rust/rustffi"
TARGET_DIR="$WORKDIR/rt-thread/components/rust/build"
RTT_APP="$WORKDIR/machines/qemu-virt-riscv64/applications"
LIBNAME="libsum.a"
LLVM_TARGET="riscv64imac-unknown-none-elf"
# LLVM_TARGET="riscv64-unknown-rtsmart"

echo "1. 编译 Rust 静态库..."
cargo build --manifest-path $RUSTAPP/Cargo.toml --target $LLVM_TARGET --target-dir $TARGET_DIR

echo "2. 复制静态库到 RT-Thread 应用目录..."
cp $TARGET_DIR/$LLVM_TARGET/debug/$LIBNAME $RTT_APP/

echo "3. 构建 RT-Thread..."
cd $WORKDIR/machines/qemu-virt-riscv64
if scons -j6; then
    echo "4. 运行 RT-Thread..."
    ./run.sh
else
    echo "RT-Thread 构建失败，返回上级目录。"
    cd $RUSTAPP
    echo "清除构建"
    cargo clean
    exit 1
fi