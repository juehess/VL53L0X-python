CC = $(CROSS_COMPILE)gcc
RM = rm

#CFLAGS = -O0 -g -Wall -c
CFLAGS = -O2 -Wall -c -fPIC

OUTPUT_DIR = bin
OBJ_DIR = obj

ROOT_DIR := $(shell pwd)
API_DIR := $(ROOT_DIR)/Api

TARGET_LIB = $(OUTPUT_DIR)/vl53l0x_python

INCLUDES = \
	-I$(ROOT_DIR) \
	-I$(API_DIR)/core/inc \
	-I$(ROOT_DIR)/platform/inc

PYTHON_INCLUDES = \
    -I/usr/include/python2.7

VPATH = \
	$(API_DIR)/core/src \
	$(ROOT_DIR)/platform/src/ \
	$(ROOT_DIR)/python_lib

LIB_SRCS = \
	vl53l0x_api_calibration.c \
	vl53l0x_api_core.c \
	vl53l0x_api_ranging.c \
	vl53l0x_api_strings.c \
	vl53l0x_api.c \
	vl53l0x_platform.c \
    vl53l0x_python.c


LIB_OBJS  = $(LIB_SRCS:%.c=$(OBJ_DIR)/%.o)

.PHONY: all
all: ${TARGET_LIB}

$(TARGET_LIB): $(LIB_OBJS)
	mkdir -p $(dir $@)
	$(CC) -shared $^ $(PYTHON_INCLUDES) $(INCLUDES) -lpthread -o $@.so

$(OBJ_DIR)/%.o:%.c
	mkdir -p $(dir $@)
	$(CC) $(CFLAGS) $(PYTHON_INCLUDES) $(INCLUDES) $< -o $@

.PHONY: clean test format quality docs docs-serve

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".eggs" -exec rm -r {} +
	find . -type d -name "build" -exec rm -r {} +
	find . -type d -name "dist" -exec rm -r {} +
	rm -rf docs/_build/

test:
	@echo "🧪 Running tests..."
	pytest

format:
	@echo "✨ Formatting code..."
	isort .
	black .

quality: format
	@echo "🔍 Checking code quality..."
	flake8 .
	pytest

.PHONY: build
build: clean
	@echo "🔨 Building C library..."
	mkdir -p $(OUTPUT_DIR)
	mkdir -p $(OBJ_DIR)
	$(MAKE) all
	@echo "📦 Installing Python package..."
	pip install -e .

.PHONY: env
env:
	@echo "🐍 Creating/updating conda environment..."
	mamba env update -f environment.yml

.PHONY: setup
setup: env build
	@echo "✅ Setup complete!"

