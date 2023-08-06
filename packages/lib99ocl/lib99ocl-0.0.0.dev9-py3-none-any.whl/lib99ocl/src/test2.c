#ifndef _TEST2_C_
#define _TEST2_C_


#define CL_TARGET_OPENCL_VERSION 120
#define CL_USE_DEPRECATED_OPENCL_1_2_APIS


#ifdef __APPLE__
#include <OpenCL/cl.h>
#else
#include <CL/cl.h>
#endif


#include <math.h>
#include <stdio.h>


#define USE_DOUBLE 1
 

double pipas(double *x, double y, double z) {
  double r = sqrt(x * x + y * y + z * z);
  double theta = acos(z / r);
  double phi = atan2(y, x);
  return r * sin(theta) * cos(phi);
}









int main() {
  cl_command_queue command_queue;
  cl_context context;
  cl_device_id device;
  cl_int input = 1;
  cl_int kernel_result = 1;
  cl_kernel kernel;
  cl_mem buffer;
  cl_platform_id platform;
  cl_program program;
  const char *source = "\
       #include <lib99ocl/core.c>\
       #include <lib99ocl/complex.c>\
       #include <lib99ocl/special.c>\
       #include <lib99ocl/cspecial.c>\
       #include <lib99ocl/lineshapes.c>\
       #include <lib99ocl/stats.c>\
       #include <lib99ocl/random.c>\
       #include <exposed/core.ocl>\
       #include <exposed/kernels.ocl>\
      __kernel void increment(int in, __global int* out) { out[0] = in + 1; }\
    ";

  clGetPlatformIDs(1, &platform, NULL);
  clGetDeviceIDs(platform, CL_DEVICE_TYPE_ALL, 0, &device, NULL);
  context = clCreateContext(NULL, 1, &device, NULL, NULL, NULL);
  command_queue = clCreateCommandQueue(context, device, 0, NULL);
  buffer = clCreateBuffer(context, CL_MEM_READ_WRITE | CL_MEM_ALLOC_HOST_PTR,
                          sizeof(cl_int), NULL, NULL);
  program = clCreateProgramWithSource(context, 1, &source, NULL, NULL);
  clBuildProgram(program, 1, &device, "", NULL, NULL);
  kernel = clCreateKernel(program, "increment", NULL);
  clSetKernelArg(kernel, 0, sizeof(cl_int), &input);
  clSetKernelArg(kernel, 1, sizeof(cl_mem), &buffer);
  clEnqueueTask(command_queue, kernel, 0, NULL, NULL);
  clFlush(command_queue);
  clFinish(command_queue);
  clEnqueueReadBuffer(command_queue, buffer, CL_TRUE, 0, sizeof(cl_int),
                      &kernel_result, 0, NULL, NULL);
  printf("result = %d\n", kernel_result);

  // assert(kernel_result == 2);
  return EXIT_SUCCESS;
}


#endif // _TEST2_C_


// vim: fdm=marker ts=2 sw=2 sts=2 sr et
