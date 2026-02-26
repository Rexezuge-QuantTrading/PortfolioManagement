import { container } from 'tsyringe';

import { UserService } from '../services/UserService';
import { UserRepository } from '../repositories/UserRepository';

// 注册依赖
container.registerSingleton(UserRepository);
container.registerSingleton(UserService);

export { container };
